// 서비스 워커 자체의 동작을 정의
// install : 서비스 워커가 브라우저에 처음 설치될 때 발생
self.addEventListener('install', (event) => {
    console.log('Service Worker installing.');
    event.waitUntil(
        caches.open('my-cache').then((cache) => {  // my-cache라는 이름으로 캐시를 열거나 새로 생성
        return cache.addAll([
            '/',
            '/index.html',
            '/app.js',
            '/style.css',
        ]);
        })
    );
});

self.addEventListener('activate', (event) => { // 서비스 워커가 설치 후 활성화될 때 발생
  console.log('Service Worker activated.');
});

self.addEventListener('fetch', (event) => { // 브라우저가 리소스를 요청할 때마다 발생
    // 캐시된 자원이 있으면 그 자원을 반환
    // 캐시된 자원이 없다면 네트워크에서 해당 자원을 fetch(요청)하여 반환
    event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
