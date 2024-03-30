<script lang="ts">
    import Header from '$lib/components/Header.svelte';
    import { goto } from '$app/navigation';
    import axios from 'axios';

    let username: string = '';
    let password: string = '';
    let email: string = '';

    const navigateTo = (url: string): void => {
        goto(url);
    };

    const sendData = async () => {
        const formData = {
            username,
            password,
            email,
        };

        try {
            const response = await axios.post('/api/register', formData);
            console.log('Data sent:', formData);
            if (response.status === 200) {
                navigateTo('/login');
            }
        } catch (error) {
            console.error('Error occurred:', error);
        }
    };
</script>

<div class="min-h-screen flex flex-col items-center justify-center">
    <Header title="Join Page" />

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

            <input
                type="email"
                placeholder="Email"
                class="px-4 py-2 border border-gray-300 rounded-md focus:outline-gray-300 focus:border-blue-500"
                bind:value={email}
                required
            />

            <button
                class="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                on:click={() => sendData()}>Join</button
            >
            <button
                class="bg-gray-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
                on:click={() => navigateTo('/')}>Cancel</button
            >
        </form>
    </section>
</div>
