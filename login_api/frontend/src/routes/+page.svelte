<script lang="ts">
    import { goto } from '$app/navigation';
    import Header from '$lib/components/Header.svelte';
    import { auth, deleteSession } from '$lib/stores/auth';

    const navigateTo = (url: string): void => {
        goto(url);
    };

    $: sessionId = $auth.sessionId;
</script>

<div class="min-h-screen flex flex-col item-center justify-center">
    <Header title="Main Page" />

    <section class="flex item-center justify-center">
        <div class="flex flex-col space-y-4">
            {#if sessionId}
                <button
                    class="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded"
                    on:click={() => {
                        navigateTo('/users');
                    }}>Select</button
                >
                <button
                    class="bg-red-300 hover:bg-red-500 text-white font-bold py-2 px-4 rounded"
                    on:click={() => {
                        deleteSession();
                        navigateTo('/login');
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
