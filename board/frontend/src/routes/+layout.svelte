<script lang="ts">
    import '../app.css';
    import { goto } from '$app/navigation';
    import { currentPage } from '../lib/store.js';

    const navigateToPage = (url: string) => {
        currentPage.set(0);
        goto(url);
    };
</script>

<div class="bg-gray-800 text-white py-4 px-4 flex justify-between items-center">
    <button class="text-lg font-semibold" on:click={() => navigateToPage('/')}>
        SHB
    </button>
</div>

<slot />
