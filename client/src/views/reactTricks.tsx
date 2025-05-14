import axios from "axios"
import { useEffect, useState, memo, useCallback, useMemo, useDeferredValue,
  useTransition } from "react"

const List = memo(({ data }: { data: string[] }) => {
  console.count("List render");
  return (
    <ul>
      {data.map((item: any, index) => (
        <li key={index}>{item}</li>
      ))}
    </ul>
  );
}, (prevProps, nextProps) => {
  return prevProps.data.length === nextProps.data.length;
})

const ReactTricks = memo(() => {
  let [data, setData] = useState<string[]>([])
  const [search, setSearch] = useState<string>("")
  // const [filteredData, setFilteredData] = useState<string[]>([])
  // const [isPending, startTransition] = useTransition()

  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await axios.get("https://restcountries.com/v3.1/all")
        const newData = res.data.
          map((item: { name: { official: string } }) => item.name.official)
        const expanded = Array(50).fill(0).flatMap(() => newData)
        setData(expanded)
        // setFilteredData(expanded)
      } catch (error) {
        console.error("Failed to fetch data:", error)
      }
    }

    fetchData()
  }, [])


  /* useDeferredValue */
  const handleSearch = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const newSearch = e.target.value
    if (newSearch !== search) {
      setSearch(newSearch)
    }
  }, [search])

  const deferredSearch = useDeferredValue(search)

  const filteredData = useMemo(() =>
    data.filter(item =>
      item.toLowerCase().includes(deferredSearch.toLowerCase())
    ), [data, deferredSearch])


  /* useTransition */
  // const handleSearch = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
  //   const newSearch = e.target.value
  //   setSearch(newSearch)

  //   startTransition(() => {
  //     const filtered = data.filter(item =>
  //       item.toLowerCase().includes(newSearch.toLowerCase())
  //     )
  //     setFilteredData(filtered)
  //   })
  // }, [data])

  console.count('Component render')

  return (
    <div>
      <h1>React Tricks</h1>
      <input type="text" value={search} onChange={handleSearch} />
      {/* {isPending && <div style={{ color: "gray" }}>⏳ Pending...</div>} */}
      {filteredData.length > 0 &&
        <List data={filteredData}/>
      }
    </div>
  )
})

export default ReactTricks