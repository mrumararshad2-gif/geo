import { useRouter } from 'next/router'
import useSWR from 'swr'
import { useState } from 'react'

const fetcher = (url: string) => fetch(url).then(res => res.json())

export default function SitePage() {
  const router = useRouter()
  const { id } = router.query
  const { data: llmsVersions, mutate } = useSWR(id ? `http://localhost:8000/sites/${id}/llms` : null, fetcher)
  const [content, setContent] = useState('User-agent: *\nDisallow: /private')

  const addVersion = async () => {
    await fetch(`http://localhost:8000/sites/${id}/llms`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })
    mutate()
  }

  return (
    <div style={{ padding: 32 }}>
      <h1>LLMS.txt Versions</h1>
      <textarea rows={6} cols={60} value={content} onChange={e => setContent(e.target.value)} />
      <br />
      <button onClick={addVersion}>Save Version</button>

      <ul>
        {llmsVersions?.map((v: any) => (
          <li key={v.id}>
            {new Date(v.created_at).toLocaleString()} <pre>{v.content}</pre>
          </li>
        ))}
      </ul>
    </div>
  )
}