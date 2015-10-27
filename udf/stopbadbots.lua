-- generic map with all bins
local function map_generic(rec)
    local names = record.bin_names(rec)
    local ret = map{}
    for i, name in ipairs(names) do
        ret[name] = rec[name]
    end
    return ret
end

-- reduce timestamp
local function reduce_timestamp(timestamp, new_interval)
    --timestamp = timestamp - 3600
    -- print(os.date("Before %c", timestamp))
    date = os.date("*t", timestamp)
    seconds = (date['min'] + date['hour']*60)*60
    diff = seconds % (new_interval*60)
    -- print(os.date("After %c", timestamp - diff))
    return timestamp - diff
end


-- distinct
-- equivalent to SELECT distinct(bin), bin FROM XXX
-- takes bin as parameter and returns all distinct values
function distinct(stream, bin)

  local function mapper(rec)
      local ret = map{}
      ret[bin] = rec[bin]
      return ret
  end

  local function accumulate(currentList, nextElement)
    local key = nextElement[bin]
    if currentList[key] == nil then
      currentList[key] = 1
    end
    return currentList
  end

  local function mymerge(a, b)
    return a
  end

  local function reducer(this, that)
    return map.merge(this, that, mymerge)
  end

  return stream : map(mapper) : aggregate(map{}, accumulate) : reduce(reducer)
end


-- group_by_count
-- equivalent to SELECT count(*), bin FROM XXX GROUP BY bin
-- takes bin as parameter and returns a map {binval: num_ocurrences}
function group_by_count(stream, bin)
  local function mapper(rec)
      local ret = map{}
      ret[bin] = rec[bin]
      return ret
  end

  local function accumulate(currentList, nextElement)
    local key = nextElement[bin]
    if currentList[key] == nil then
      currentList[key] = 1
    else
      currentList[key] = currentList[key] + 1
    end
    return currentList
  end

  local function mymerge(a, b)
    return a+b
  end

  local function reducer(this, that)
    return map.merge(this, that, mymerge)
  end

  return stream : map(mapper) : aggregate(map{}, accumulate) : reduce(reducer)
end

----


function filter_equal(stream, bin, value)
  local function filter_regular(record)
    return record[bin] == value
  end
  return stream : filter(filter_regular) : map(map_generic)
end

function filter_range(stream, bin, min, max)
  local function filter_range(record)
    return record[bin] >= min and record[bin] <= max
  end
  return stream : filter(filter_range) : map(map_generic)
end