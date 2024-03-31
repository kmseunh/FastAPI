<script lang="ts">
    import { cookieStore } from '$lib/stores/auth';
    import { goto } from '$app/navigation';
    import Header from '$lib/components/Header.svelte';
    import axios from 'axios';

    $: cookie = $cookieStore;

    const navigateTo = (url: string): void => {
        goto(url);
    };

    const logout = async (): Promise<void> => {
        try {
            const response = await axios.delete('api/logout', {
                headers: { cookie },
            }); // 로그아웃 엔드포인트에 POST 요청
            if (response.status === 200) {
                cookieStore.set(null); // 쿠키 상태 업데이트
                navigateTo('/login'); // 로그인 페이지로 이동
            } else {
                throw new Error('Logout failed');
            }
        } catch (error) {
            console.error('Error occurred during logout:', error);
        }
    };
</script>

<div class="min-h-screen flex flex-col item-center justify-center">
    <Header title="Main Page" />

    <section class="flex item-center justify-center">
        <div class="flex flex-col space-y-4">
            {#if cookie}
                <button
                    class="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded"
                    on:click={() => {
                        navigateTo('/users');
                    }}>Select</button
                >
                <button
                    class="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded"
                    on:click={() => {
                        logout();
                    }}>Logout</button
                >
            {:else}
                <button
                    class="bg-blue-300 hover:bg-blue-500 text-white font-bold py-2 px-4 rounded"
                    on:click={() => navigateTo('/login')}>Login</button
                >
                <button
                    class="bg-gray-300 hover:bg-gray-500 text-white font-bold py-2 px-4 rounded"
                    on:click={() => navigateTo('/join')}>Join</button
                >
            {/if}
        </div>
    </section>
</div>
