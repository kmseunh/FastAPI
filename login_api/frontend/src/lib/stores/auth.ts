import { writable } from 'svelte/store';
import axios from 'axios';

export const getCookie = (): string | null => {
    return typeof window !== 'undefined' ? document.cookie : null;
};

export const cookieStore = writable<string | null>(getCookie());

cookieStore.subscribe((value) => {
    console.log('Cookie updated:', value);
});

export const fetchProtectedResource = async (): Promise<void> => {
    try {
        const cookie = getCookie();
        if (!cookie) {
            throw new Error('Cookie not found');
        }
        const response = await axios.get('/api/protected_resource', {
            headers: {
                Cookie: `session_id=${cookie}`,
            },
        });
        console.log(response.data);
    } catch (error) {
        console.error('Error occurred:', error);
    }
};
