<script lang="ts">
    import { goto } from '$app/navigation';
    import fastapi from '$lib/api';
    import { onMount } from 'svelte';

    interface Question {
        id: number;
        subject: string;
        content: string;
        create_date: string;
    }

    let question_list: Question[] = [];

    async function fetchQuestionList(): Promise<void> {
        fastapi('get', '/api/question/list', {}, (json: Question[]) => {
            question_list = json.map((question) => ({
                ...question,
                create_date: formatDate(question.create_date),
            }));
        });
    }

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

    onMount(fetchQuestionList);
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

<div class="max-w-md mx-auto mt-4 text-center">
    <button
        class="px-4 py-2 border border-gray-300 rounded hover:bg-gray-100 focus:outline-none"
        on:click={navigateToQuestionForm}
    >
        질문 등록하기
    </button>
</div>
