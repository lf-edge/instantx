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

import { useCallback, useEffect, useState } from 'react'

export type Theme = 'dark' | 'light'

/**
 * Owns theme toggling after the pre-paint script in index.html has set the
 * initial `data-theme`. localStorage is only written on an explicit toggle,
 * so first-time visitors keep following their OS preference.
 */
export function useTheme(): [Theme, () => void] {
  const [theme, setTheme] = useState<Theme>(() =>
    document.documentElement.getAttribute('data-theme') === 'light' ? 'light' : 'dark',
  )

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
    document
      .getElementById('metaTheme')
      ?.setAttribute('content', theme === 'light' ? '#fcfbfd' : '#0d0911')
  }, [theme])

  const toggle = useCallback(() => {
    setTheme((prev) => {
      const next = prev === 'light' ? 'dark' : 'light'
      try {
        localStorage.setItem('ix-theme', next)
      } catch {
        // storage unavailable (private mode) — theme just won't persist
      }
      return next
    })
  }, [])

  return [theme, toggle]
}
