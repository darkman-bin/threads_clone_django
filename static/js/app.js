/* Threadify JS
   - Toggle dark mode (Bootstrap data-bs-theme)
   - AJAX Like / Follow with CSRF
*/

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) return parts.pop().split(';').shift();
  return null;
}

async function postJSON(url, data) {
  const csrftoken = getCookie('csrftoken');
  const res = await fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': csrftoken,
      'X-Requested-With': 'XMLHttpRequest',
    },
    body: JSON.stringify(data || {}),
  });
  return { ok: res.ok, status: res.status, data: await res.json().catch(() => ({})) };
}

function initThemeToggle() {
  const toggle = document.getElementById('themeToggle');
  if (!toggle) return;

  const root = document.documentElement;
  const saved = localStorage.getItem('theme') || 'light';
  root.setAttribute('data-bs-theme', saved);

  toggle.addEventListener('click', () => {
    const current = root.getAttribute('data-bs-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    root.setAttribute('data-bs-theme', next);
    localStorage.setItem('theme', next);
  });
}

function initLikeButtons() {
  document.querySelectorAll('.js-like').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const id = btn.getAttribute('data-thread-id');
      if (!id) return;

      const url = `/t/${id}/like/`;
      const result = await postJSON(url, {});
      if (!result.ok) return;

      const liked = result.data.liked;
      const count = result.data.likes_count;

      btn.setAttribute('data-liked', liked ? '1' : '0');
      const icon = btn.querySelector('i.bi');
      const countEl = btn.querySelector('.js-like-count');

      if (icon) {
        icon.classList.remove('bi-heart', 'bi-heart-fill');
        icon.classList.add(liked ? 'bi-heart-fill' : 'bi-heart');
      }
      if (countEl) countEl.textContent = count;
    });
  });
}

function initFollowButtons() {
  document.querySelectorAll('.js-follow').forEach((btn) => {
    btn.addEventListener('click', async (e) => {
      e.preventDefault();
      const username = btn.getAttribute('data-username');
      if (!username) return;

      const url = `/u/${username}/follow/`;
      const result = await postJSON(url, {});
      if (!result.ok) return;

      const following = result.data.following;
      btn.setAttribute('data-following', following ? '1' : '0');

      const icon = btn.querySelector('i.bi');
      if (icon) {
        icon.classList.remove('bi-person-plus', 'bi-person-dash');
        icon.classList.add(following ? 'bi-person-dash' : 'bi-person-plus');
      }

      // Text
      btn.innerHTML = following
        ? '<i class="bi bi-person-dash"></i> إلغاء متابعة'
        : '<i class="bi bi-person-plus"></i> متابعة';

      // Followers count
      const fc = document.getElementById('followersCount');
      if (fc && typeof result.data.followers_count === 'number') {
        fc.textContent = result.data.followers_count;
      }
    });
  });
}

document.addEventListener('DOMContentLoaded', () => {
  initThemeToggle();
  initLikeButtons();
  initFollowButtons();
});
