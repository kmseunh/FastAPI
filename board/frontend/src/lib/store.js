import { writable } from 'svelte/store';

// 페이지 스토어를 생성하고 초기값을 0으로 설정합니다.
export const currentPage = writable(0);

// 클라이언트 사이드에서만 localStorage를 사용하여 페이지 값을 유지합니다.
if (typeof window !== 'undefined') {
    const storedPage = localStorage.getItem('storedPage');
    if (storedPage !== null) {
        currentPage.set(parseInt(storedPage));
    }

    // 현재 페이지가 변경될 때마다 localStorage에 저장합니다.
    currentPage.subscribe((value) => {
        localStorage.setItem('storedPage', value.toString());
    });
}
