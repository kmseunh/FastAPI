<script lang="ts">
    import fastapi from '$lib/api';
    import { goto } from '$app/navigation';
    import type { PageData } from './$types';

    export let data: PageData;

    let question_id: number;
    let answers: Array<{ content: string; create_date: string }>;
    let content: string = '';
    let errMessage: string = '';
    let answerCount = data.answers.length;

    // 페이지 데이터가 변경될 때마다 해당 데이터를 업데이트합니다.
    $: {
        question_id = data.id;
        answers = data.answers;
    }

    const postAnswer = async (event: Event) => {
        event.preventDefault();

        if (!content.trim()) {
            errMessage = '빈 값을 허용하지 않습니다.';
            return;
        }

        let url = `/api/answer/create/${question_id}`;

        try {
            await fastapi('post', url, { content });
            console.log('Answer submitted successfully');
            location.reload();
        } catch (error) {
            console.error('Error submitting answer:', error);
            // 에러 처리를 추가할 수 있습니다.
        }
    };

    const formatDate = (dateString: string): string => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };
</script>

<div class="max-w-2xl mx-auto mt-8">
    <h1 class="text-3xl font-bold text-gray-800 mb-4 border-b pb-2">
        {data.subject}
    </h1>
    <div class="mb-4 p-4 border rounded-lg shadow-sm bg-white">
        {data.content}
    </div>
    <button
        class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:border-blue-300"
        on:click={() => goto('/')}>목록으로</button
    >
    <h2 class="text-2xl font-bold mb-4 mt-6">
        {answerCount}개의 답변이 있습니다.
    </h2>
    <ul>
        {#each answers as answer}
            <li class="mb-4 p-4 border rounded-lg shadow-sm bg-white">
                {answer.content}
                <p class="text-sm text-gray-500">
                    {formatDate(answer.create_date)}
                </p>
            </li>
        {/each}
    </ul>

    {#if errMessage}
        <p class="mt-4 text-red-500">{errMessage}</p>
    {/if}

    <!-- 답변 입력 폼 -->
    <form class="mt-8" on:submit={postAnswer}>
        <textarea
            class="w-full px-3 py-2 text-gray-700 border rounded-md focus:outline-none focus:ring focus:border-blue-500"
            rows="6"
            bind:value={content}
            placeholder="내용을 입력하세요..."
        ></textarea>
        <button
            type="submit"
            class="mt-4 px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 focus:outline-none focus:ring focus:border-blue-300"
            >답변 등록</button
        >
    </form>
</div>
