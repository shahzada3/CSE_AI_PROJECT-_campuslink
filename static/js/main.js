// ===== THEME TOGGLE =====
const htmlRoot = document.getElementById('html-root');
const themeIcon = document.getElementById('theme-icon');
const themeLabel = document.getElementById('theme-label');

function applyTheme(dark) {
  if (dark) {
    document.body.classList.add('dark-mode');
    if (themeIcon) { themeIcon.classList.remove('fa-moon'); themeIcon.classList.add('fa-sun'); }
    if (themeLabel) themeLabel.textContent = 'Light Mode';
  } else {
    document.body.classList.remove('dark-mode');
    if (themeIcon) { themeIcon.classList.remove('fa-sun'); themeIcon.classList.add('fa-moon'); }
    if (themeLabel) themeLabel.textContent = 'Dark Mode';
  }
}

function toggleTheme() {
  const isDark = document.body.classList.contains('dark-mode');
  localStorage.setItem('campusTheme', isDark ? 'light' : 'dark');
  applyTheme(!isDark);
}

// Load saved theme on page load
(function() {
  const saved = localStorage.getItem('campusTheme');
  if (saved === 'light') {
    applyTheme(false);
  } else {
    applyTheme(true); // default dark
  }
})();


// ===== LIKE POST =====
function likePost(postId, btn) {
  fetch(`/posts/like/${postId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/json',
    },
  })
  .then(r => r.json())
  .then(data => {
    btn.classList.toggle('liked', data.liked);
    const countEl = btn.querySelector('.like-count');
    if (countEl) countEl.textContent = data.count;
  });
}


// ===== TOGGLE COMMENTS =====
function toggleComments(postId) {
  const section = document.getElementById(`comments-${postId}`);
  if (section) section.classList.toggle('open');
}


// ===== ADD COMMENT =====
function addComment(postId) {
  const input = document.getElementById(`comment-input-${postId}`);
  const content = input.value.trim();
  if (!content) return;

  fetch(`/posts/comment/${postId}/`, {
    method: 'POST',
    headers: {
      'X-CSRFToken': getCookie('csrftoken'),
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: `content=${encodeURIComponent(content)}`,
  })
  .then(r => r.json())
  .then(data => {
    if (data.success) {
      const list = document.getElementById(`comment-list-${postId}`);
      const div = document.createElement('div');
      div.className = 'comment-item';
      div.innerHTML = `
        <div class="comment-avatar">${data.username[0].toUpperCase()}</div>
        <div class="comment-bubble">
          <div class="comment-name">${data.username}</div>
          <div class="comment-text">${data.content}</div>
        </div>`;
      list.appendChild(div);
      input.value = '';
    }
  });
}


// ===== CSRF COOKIE =====
function getCookie(name) {
  let v = null;
  document.cookie.split(';').forEach(c => {
    c = c.trim();
    if (c.startsWith(name + '=')) v = decodeURIComponent(c.slice(name.length + 1));
  });
  return v;
}


// ===== AUTO RESIZE TEXTAREA =====
document.querySelectorAll('textarea.composer-input').forEach(el => {
  el.addEventListener('input', function() {
    this.style.height = 'auto';
    this.style.height = Math.min(this.scrollHeight, 120) + 'px';
  });
});


// ===== AUTO SCROLL CHAT =====
const chatMessages = document.getElementById('chat-messages');
if (chatMessages) {
  chatMessages.scrollTop = chatMessages.scrollHeight;
}
const groupMessages = document.getElementById('group-messages');
if (groupMessages) {
  groupMessages.scrollTop = groupMessages.scrollHeight;
}



// ===== ESCAPE HTML =====
function escapeHtml(text) {
  const d = document.createElement('div');
  d.appendChild(document.createTextNode(text));
  return d.innerHTML;
}


// ===== AUTO DISMISS ALERTS =====
setTimeout(() => {
  document.querySelectorAll('.alert').forEach(a => a.remove());
}, 4000);