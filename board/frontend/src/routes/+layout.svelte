<script lang="ts">
    import '../app.css';
    import { goto } from '$app/navigation';

    const navigateToPage = (url: string) => {
        goto(url);
    };
</script>

<div class="bg-gray-800 text-white py-4 px-4 flex justify-between items-center">
    <button class="text-lg font-semibold" on:click={() => navigateToPage('/')}>
        SHB
    </button>
    <div class="flex space-x-4">
        <button
            class="hover:text-gray-300"
            on:click={() => navigateToPage('/user-login')}>로그인</button
        >
        <button
            class="hover:text-gray-300"
            on:click={() => navigateToPage('/user-create')}>회원가입</button
        >
    </div>
</div>

<slot />
