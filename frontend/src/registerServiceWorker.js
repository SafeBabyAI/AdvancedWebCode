/* eslint-disable no-console */
// 서비스 워커를 등록
import { register } from 'register-service-worker'

if (process.env.NODE_ENV === 'production') { // process.env.NODE_ENV가 'production'인 경우에만 서비스 워커가 등록
  register(`${process.env.BASE_URL}service-worker.js`, {
    ready () { // 서비스 워커를 등록하는 함수로, 서비스 워커의 경로(service-worker.js)를 인자로 받음
      console.log(
        'App is being served from cache by a service worker.\n' +
        'For more details, visit https://goo.gl/AFskqB'
      )
    },
    registered () {
      console.log('Service worker has been registered.')
    },
    cached () {
      console.log('Content has been cached for offline use.')
    },
    updatefound () {
      console.log('New content is downloading.')
    },
    updated () {
      console.log('New content is available; please refresh.')
    },
    offline () {
      console.log('No internet connection found. App is running in offline mode.')
    },
    error (error) {
      console.error('Error during service worker registration:', error)
    }
  })
}
