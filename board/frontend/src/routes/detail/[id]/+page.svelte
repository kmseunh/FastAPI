<script lang="ts">
    import fastapi from '$lib/api';
    import type { PageData } from './$types';

    export let data: PageData;
    console.log(data);

    let question_id = data.id;
    let answers = data.answers;
    let content: string;
    let errorMessage: string | null = null;

    const post_answer = (event: Event) => {
        event.preventDefault();
        let url = '/api/answer/create/' + question_id;
        console.log(url);
        let params = {
            content: content,
        };
        fastapi(
            'post',
            url,
            params,
            (data) => {
                console.log('Answer submitted successfully:', data);
            },
            (error) => {
                console.error('Error submitting answer:', error);
                errorMessage = error.detail[0]['msg'];
                console.log(errorMessage);
            }
        );
    };
</script>

<!-- Tailwind CSS를 사용하여 스타일 적용 -->
<div class="max-w-2xl mx-auto mt-8">
    <h1 class="text-3xl font-bold">{data.subject}</h1>
    <div class="mt-4">{data.content}</div>
    <ul class="mt-4">
        {#each answers as answer}
            <li>{answer.content}</li>
        {/each}
    </ul>
    {#if errorMessage}
        <p class="mt-4 text-red-500">{errorMessage}</p>
        <!-- Displaying error message if exists -->
    {/if}
    <form class="mt-8" method="post">
        <textarea
            class="w-full px-3 py-2 text-black border rounded-md"
            rows="6"
            bind:value={content}
            placeholder="내용을 입력하세요..."
        ></textarea>
        <button
            type="submit"
            class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600"
            on:click={post_answer}>답변 등록</button
        >
    </form>
</div>
