const CACHE = 'wrexa-v1';
const STATIC = ['/', '/css/main.css', '/js/main.js', '/award-nomination'];
self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(STATIC)));
});
self.addEventListener('fetch', e => {
  e.respondWith(caches.match(e.request).then(r => r || fetch(e.request)));
});
