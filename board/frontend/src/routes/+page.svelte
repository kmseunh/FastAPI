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
            question_list = json;
        });
    }

    const navigateToDetailPage = (id: number) => {
        goto(`/detail/${id}`);
    };

    onMount(fetchQuestionList);
</script>

<!-- 게시판 미니멀 스타일링 -->
<div class="max-w-md mx-auto mt-8">
    <ul class="divide-y divide-gray-200">
        {#each question_list as question}
            <li>
                <button
                    class="block w-full py-4 text-left hover:bg-gray-100 focus:outline-none"
                    on:click={() => navigateToDetailPage(question.id)}
                >
                    <h2 class="text-lg font-semibold text-blue-500">
                        {question.subject}
                    </h2>
                    <p class="mt-2 text-sm text-gray-600">
                        {question.create_date}
                    </p>
                </button>
            </li>
        {/each}
    </ul>
</div>
