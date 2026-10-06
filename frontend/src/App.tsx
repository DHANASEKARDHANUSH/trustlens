import { useEffect, useState } from 'react'

type Health = { status: string; service: string }

const apiBase = import.meta.env.VITE_API_BASE_URL ?? 'http://localhost:8000'

export default function App() {
  const [health, setHealth] = useState<'checking' | 'online' | 'offline'>('checking')

  useEffect(() => {
    fetch(`${apiBase}/api/health`)
      .then((response) => {
        if (!response.ok) throw new Error('API unavailable')
        return response.json() as Promise<Health>
      })
      .then((data) => setHealth(data.status === 'ok' ? 'online' : 'offline'))
      .catch(() => setHealth('offline'))
  }, [])

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/" aria-label="TrustLens home"><span className="brand-mark">T</span> TrustLens</a>
        <span className="status"><i className={`status-dot ${health}`} /> API {health}</span>
      </header>
      <section className="hero" aria-labelledby="headline">
        <p className="eyebrow">INDEPENDENT INVESTIGATION, GROUNDED IN EVIDENCE</p>
        <h1 id="headline">Don’t trust the internet.<br /><em>Investigate it.</em></h1>
        <p className="intro">Check a product, business, or opportunity against evidence from across the web.</p>
        <form className="investigation-form" onSubmit={(event) => event.preventDefault()}>
          <label htmlFor="investigation">What would you like to investigate?</label>
          <textarea id="investigation" placeholder="e.g. Is this RTX 4060 laptop deal for ₹9,999 legitimate?" rows={3} />
          <div className="form-footer">
            <span>Product · Business · Job or internship</span>
            <button type="submit" disabled>Start investigation <span aria-hidden="true">→</span></button>
          </div>
        </form>
        <p className="phase-note">Investigation workspace</p>
      </section>
      <footer><span>Evidence first. Conclusions with sources.</span><span>TrustLens · Research preview</span></footer>
    </main>
  )
}
