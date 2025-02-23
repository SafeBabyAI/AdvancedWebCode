// 📌 서비스 워커 설치 (install) 이벤트
self.addEventListener("install", (event) => {
  console.log("Service Worker installing...");

  event.waitUntil(
    caches.open("my-cache").then((cache) => {
      console.log("캐시 저장 시작");
      return cache.addAll([
        "/",
        "/index.html",
        "/app.js",
        "/style.css",
        "/icon-192x192.png",
        "/icon-512x512.png"
      ]);
    })
  );
});

// 📌 서비스 워커 활성화 (activate) 이벤트
self.addEventListener("activate", (event) => {
  console.log("Service Worker activated.");
});

// 📌 fetch 이벤트 처리 (캐시 우선, 없으면 네트워크 요청)
self.addEventListener("fetch", (event) => {
  event.respondWith(
    caches.match(event.request).then((cachedResponse) => {
      return cachedResponse || fetch(event.request);
    })
  );
});
