/* ========================LICENSE_START=================================
 * InstantX Website
 * %%
 * Copyright (C) 2024 - 2026 Vodafone
 * %%
 * Licensed under the MIT License;
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *      https://opensource.org/license/mit
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 * =========================LICENSE_END==================================
 */

import { useState } from 'react'
import logoDark from '../assets/instantx-logo-dark.png'
import logoLight from '../assets/instantx-logo.png'
import { useGitHubStars } from '../hooks/useGitHubStars'
import { useScrollSpy } from '../hooks/useScrollSpy'
import { useTheme } from '../hooks/useTheme'
import { GitHubIcon } from './icons'

const NAV_LINKS = [
  { id: 'features', label: 'Features' },
  { id: 'architecture', label: 'Architecture' },
  { id: 'quickstart', label: 'Quick start' },
  { id: 'contribute', label: 'Contribute' },
  { id: 'docs', label: 'Docs' },
] as const

const OBSERVED_SECTIONS = ['features', 'architecture', 'quickstart', 'contribute'] as const

function Header() {
  const [theme, toggleTheme] = useTheme()
  const [menuOpen, setMenuOpen] = useState(false)
  const activeId = useScrollSpy(OBSERVED_SECTIONS)
  const stars = useGitHubStars()
  const light = theme === 'light'

  return (
    <header className="site-header">
      <nav className="nav wrap" aria-label="Primary">
        <a className="brand" href="#top" aria-label="InstantX home">
          <img className="brand-logo brand-logo--dark" src={logoDark} width={780} height={192} alt="" />
          <img className="brand-logo brand-logo--light" src={logoLight} width={780} height={192} alt="" />
        </a>
        <div className={`nav-links${menuOpen ? ' open' : ''}`} id="navLinks">
          {NAV_LINKS.map(({ id, label }) => (
            <a
              key={id}
              href={`#${id}`}
              className={activeId === id ? 'active' : undefined}
              onClick={() => setMenuOpen(false)}
            >
              {label}
            </a>
          ))}
        </div>
        <div className="nav-right">
          <button
            className="icon-btn"
            id="themeBtn"
            aria-label={light ? 'Switch to dark theme' : 'Switch to light theme'}
            aria-pressed={light}
            onClick={toggleTheme}
          >
            <svg
              className="icon-sun"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              aria-hidden="true"
            >
              <circle cx="12" cy="12" r="4.5" />
              <path d="M12 2v2M12 20v2M2 12h2M20 12h2M5 5l1.5 1.5M17.5 17.5 19 19M19 5l-1.5 1.5M6.5 17.5 5 19" />
            </svg>
            <svg
              className="icon-moon"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              aria-hidden="true"
            >
              <path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8Z" />
            </svg>
          </button>
          <span className="gh-star">
            <a className="gh-main" href="https://github.com/lf-edge/instantx" target="_blank" rel="noopener">
              <GitHubIcon /> Star
            </a>
            <span className="gh-count" title="Stars on GitHub">★ {stars ?? '16'}</span>
          </span>
          <button
            className="icon-btn nav-toggle"
            aria-label={menuOpen ? 'Close menu' : 'Open menu'}
            aria-expanded={menuOpen}
            aria-controls="navLinks"
            onClick={() => setMenuOpen((open) => !open)}
          >
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" aria-hidden="true">
              <path d="M3 6h18M3 12h18M3 18h18" />
            </svg>
          </button>
        </div>
      </nav>
    </header>
  )
}

export default Header
