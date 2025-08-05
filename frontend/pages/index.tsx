import useSWR from 'swr'
import { useState } from 'react'
import Link from 'next/link'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function Home() {
  const { data: sites, mutate } = useSWR('http://localhost:8000/sites', fetcher)
  const [domain, setDomain] = useState('')

  const addSite = async () => {
    await fetch('http://localhost:8000/sites', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ domain })
    })
    setDomain('')
    mutate()
  }

  const crawlSite = async (id: number) => {
    await fetch(`http://localhost:8000/sites/${id}/crawl`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ depth: 1 })
    })
  }

  return (
    <div style={{ padding: 32 }}>
      <h1>GEO SaaS</h1>
      <input value={domain} onChange={e => setDomain(e.target.value)} placeholder="example.com" />
      <button onClick={addSite}>Add Site</button>

      <h2>Sites</h2>
      <ul>
        {sites?.map((s: any) => (
          <li key={s.id}>
            <Link href={`/sites/${s.id}`}>{s.domain}</Link> <button onClick={() => crawlSite(s.id)}>Crawl</button>
          </li>
        ))}
      </ul>
    </div>
  )
}