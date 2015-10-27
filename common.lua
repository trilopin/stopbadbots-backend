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