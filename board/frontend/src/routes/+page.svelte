<script lang="ts">
    import { goto } from '$app/navigation';
    import fastapi from '$lib/api';
    import { onMount } from 'svelte';

    let size = 10;
    let page = 0;
    let total = 0;
    let total_page = 0;

    interface Question {
        id: number;
        subject: string;
        content: string;
        create_date: string;
    }

    let question_list: Question[] = [];

    const fetchQuestionList = async (_page: number): Promise<void> => {
        const params = { page: _page, size: size };
        const json = await fastapi('get', '/api/question/list', params);
        question_list = json.question_list.map((question: Question) => ({
            ...question,
            create_date: formatDate(question.create_date),
        }));
        page = _page;
        total = json.total;
        total_page = Math.ceil(total / size);
    };

    const navigateToDetailPage = (id: number) => {
        goto(`/detail/${id}`);
    };

    const navigateToQuestionForm = () => {
        goto('/question-form');
    };

    const formatDate = (dateString: string): string => {
        const date = new Date(dateString);
        return date.toLocaleString();
    };

    onMount(() => fetchQuestionList(0));
</script>

<div class="max-w-screen-lg mx-auto px-4 mt-8">
    <ul class="divide-y divide-gray-200">
        {#each question_list as question}
            <li class="py-4">
                <button
                    class="w-full px-4 text-left hover:bg-gray-100 focus:outline-none"
                    on:click={() => navigateToDetailPage(question.id)}
                >
                    <div class="flex justify-between items-center">
                        <h2 class="text-lg font-semibold text-blue-500">
                            {question.subject}
                        </h2>
                        <p class="text-sm text-gray-600">
                            {question.create_date}
                        </p>
                    </div>
                </button>
            </li>
        {/each}
    </ul>
</div>

<div class="flex justify-center my-4">
    <ul class="pagination flex space-x-2">
        <li class="page-item {page <= 0 && 'disabled'}">
            <button
                class="page-link"
                disabled={page <= 0}
                on:click={() => fetchQuestionList(page - 1)}>이전</button
            >
        </li>
        {#each Array(total_page) as _, loop_page}
            <li class="page-item {loop_page === page && 'active'}">
                <button
                    class="page-link bg-white border border-gray-300 rounded-full px-3 py-1 text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-gray-500"
                    disabled={loop_page === page}
                    on:click={() => fetchQuestionList(loop_page)}
                >
                    {loop_page + 1}
                </button>
            </li>
        {/each}
        <li
            class="page-item {page >= total_page - 1 ||
                ((page + 1) * size >= total && 'disabled')}"
        >
            <button
                class="page-link"
                disabled={page >= total_page - 1 || (page + 1) * size >= total}
                on:click={() => fetchQuestionList(page + 1)}
            >
                다음
            </button>
        </li>
    </ul>
</div>

<div class="max-w-md mx-auto mt-4 text-center">
    <button
        class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 focus:outline-none"
        on:click={navigateToQuestionForm}
    >
        질문 등록하기
    </button>
</div>

{#if total_page === 0}
    <p class="text-center mt-4">표시할 항목이 없습니다.</p>
{/if}
