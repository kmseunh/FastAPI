import { writable, type Writable } from 'svelte/store';
import axios, { type AxiosResponse } from 'axios';

const getSessionId = (): string | null => {
    return typeof window !== 'undefined'
        ? localStorage.getItem('sessionId')
        : null;
};

const setSessionId = (sessionId: string): void => {
    if (typeof window !== 'undefined') {
        localStorage.setItem('sessionId', sessionId);
    }
};

export const deleteSessionId = () => {
    if (typeof window !== 'undefined') {
        localStorage.removeItem('sessionId');
    }
};

interface AuthStore {
    sessionId: string | null;
}

const initialSessionId = getSessionId();

export const auth: Writable<AuthStore> = writable({
    sessionId: initialSessionId,
});

export const updateAuth = (sessionId: string) => {
    setSessionId(sessionId);
    auth.update((value) => ({ ...value, sessionId }));
};

export const deleteSession = (): void => {
    deleteSessionId();
    auth.update((value) => ({ ...value, sessionId: null }));
};

export const fetchProtectedResource = async (): Promise<void> => {
    try {
        const sessionId = getSessionId();
        if (!sessionId) {
            throw new Error('Session ID not found');
        }
        const headers = { Authorization: `Bearer ${sessionId}` };
        const response: AxiosResponse = await axios.get(
            '/api/protected_resource',
            {
                headers,
            }
        );
        console.log(response.data);
    } catch (error) {
        console.error('Error occurred:', error);
    }
};
