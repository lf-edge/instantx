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

import { useEffect, useState } from 'react'

const REPO_API = 'https://api.github.com/repos/lf-edge/instantx'

function formatStars(n: number): string {
  return n >= 1000 ? `${(n / 1000).toFixed(1).replace(/\.0$/, '')}k` : String(n)
}

/**
 * Live star count from the GitHub API. Returns null while loading or when the
 * request fails (offline, rate-limited) — callers render a static snapshot.
 */
export function useGitHubStars(): string | null {
  const [stars, setStars] = useState<string | null>(null)

  useEffect(() => {
    const controller = new AbortController()
    fetch(REPO_API, { signal: controller.signal })
      .then((r) => (r.ok ? r.json() : null))
      .then((d) => {
        if (d && typeof d.stargazers_count === 'number') {
          setStars(formatStars(d.stargazers_count))
        }
      })
      .catch(() => {
        // offline or rate-limited — keep the static count
      })
    return () => controller.abort()
  }, [])

  return stars
}
