<script lang="ts">
    import { fetchProtectedResource } from '$lib/stores/auth';
    import { onMount } from 'svelte';
    import { load } from './+page';

    interface User {
        user_id: number;
        username: string;
        email: string;
    }

    let users: User[] = [];
    let isLoading = true;

    onMount(async () => {
        try {
            await fetchProtectedResource();
            const data = await load();
            users = data.users;
        } catch (error) {
            console.error('Error fetching data:', error);
        } finally {
            isLoading = false;
        }
    });
</script>

<h1>User List</h1>

{#if isLoading}
    <p>Loading...</p>
{:else if users.length === 0}
    <p>No users found.</p>
{:else}
    {#each users as user}
        <div>
            <p>User ID: {user.user_id}</p>
            <p>Username: {user.username}</p>
            <p>Email: {user.email}</p>
        </div>
    {/each}
{/if}
