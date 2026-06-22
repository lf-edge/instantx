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

import { useRef, useState, type KeyboardEvent, type ReactNode } from 'react'

export interface TabDef {
  id: string
  label: ReactNode
  panel: ReactNode
}

interface TabsProps {
  tabs: TabDef[]
  ariaLabel: string
}

/**
 * ARIA tabs with a roving tabindex: only the selected tab is in the tab
 * order, and ArrowLeft/ArrowRight move focus and selection together.
 */
function Tabs({ tabs, ariaLabel }: TabsProps) {
  const [activeId, setActiveId] = useState(tabs[0]?.id)
  const tabRefs = useRef<(HTMLButtonElement | null)[]>([])

  function handleKeyDown(e: KeyboardEvent<HTMLButtonElement>, i: number) {
    let next: number
    if (e.key === 'ArrowRight') next = (i + 1) % tabs.length
    else if (e.key === 'ArrowLeft') next = (i - 1 + tabs.length) % tabs.length
    else return
    e.preventDefault()
    tabRefs.current[next]?.focus()
    setActiveId(tabs[next].id)
  }

  return (
    <div className="tabs">
      <div className="tab-row" role="tablist" aria-label={ariaLabel}>
        {tabs.map((tab, i) => {
          const selected = tab.id === activeId
          return (
            <button
              key={tab.id}
              ref={(el) => {
                tabRefs.current[i] = el
              }}
              className="tab"
              role="tab"
              id={`tab-${tab.id}`}
              aria-controls={`panel-${tab.id}`}
              aria-selected={selected}
              tabIndex={selected ? 0 : -1}
              onClick={() => setActiveId(tab.id)}
              onKeyDown={(e) => handleKeyDown(e, i)}
            >
              {tab.label}
            </button>
          )
        })}
      </div>
      {tabs.map((tab) => {
        const selected = tab.id === activeId
        return (
          <div
            key={tab.id}
            className={`tab-panel${selected ? ' show' : ''}`}
            id={`panel-${tab.id}`}
            role="tabpanel"
            aria-labelledby={`tab-${tab.id}`}
            hidden={!selected}
          >
            {tab.panel}
          </div>
        )
      })}
    </div>
  )
}

export default Tabs
