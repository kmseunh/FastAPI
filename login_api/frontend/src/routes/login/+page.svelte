<script lang="ts">
    import { goto } from '$app/navigation';
    import Header from '$lib/components/Header.svelte';
    import { cookieStore, getCookie } from '$lib/stores/auth';
    import axios from 'axios';

    let username: string = '';
    let password: string = '';

    const navigateTo = (url: string): void => {
        goto(url);
    };

    const loginForm = async () => {
        const formData = {
            username,
            password,
        };

        try {
            const res = await axios.post('/api/login', formData);
            console.log(formData);
            if (res.status === 200) {
                cookieStore.set(getCookie());
                navigateTo('/');
            }
        } catch (error) {
            console.error('Error occurred:', error);
        }
    };
</script>

<div class="min-h-screen flex flex-col items-center justify-center">
    <Header title="Login Page" />

    <section class="flex items-center justify-center">
        <form class="flex flex-col space-y-4" on:submit|preventDefault>
            <input
                type="text"
                placeholder="Username"
                class="px-4 py-2 border border-gray-300 rounded-md focus:outline-none focus:border-blue-500"
                bind:value={username}
                required
            />

            <input
                type="password"
                placeholder="Password"
                class="px-4 py-2 border border-gray-300 rounded-md focus:outline-gray-300 focus:border-blue-500"
                bind:value={password}
                required
            />

            <button
                class="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                on:click={() => loginForm()}>Login</button
            >
            <button
                class="bg-gray-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                on:click={() => navigateTo('/join')}>Join</button
            >
        </form>
    </section>
</div>
