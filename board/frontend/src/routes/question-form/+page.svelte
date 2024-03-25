<script lang="ts">
    import fastapi from '$lib/api';
    import { goto } from '$app/navigation';

    interface Question {
        id: number;
        subject: string;
        content: string;
        create_date: string;
    }

    let formData: Question = {
        id: 0,
        subject: '',
        content: '',
        create_date: '',
    };

    const postQuestion = async () => {
        const url = '/api/question/create';

        try {
            await fastapi('post', url, formData);
            alert('저장 되었습니다.');
            goto('/');
        } catch (error) {
            console.error('Error:', error);
        }
    };

    const handleSubmit = async (event: Event) => {
        event.preventDefault();
        await postQuestion();
    };
</script>

<div class="min-h-screen flex items-center justify-center bg-gray-100">
    <div class="max-w-4xl w-full bg-white shadow-md rounded px-10 py-8 mb-4">
        <form on:submit={handleSubmit}>
            <div class="mb-8">
                <label
                    for="subject"
                    class="block text-gray-700 text-lg font-bold mb-2"
                    >Subject:</label
                >
                <input
                    type="text"
                    id="subject"
                    class="w-full px-4 py-3 border rounded border-gray-300 focus:outline-none focus:shadow-outline"
                    bind:value={formData.subject}
                />
            </div>
            <div class="mb-8">
                <label
                    for="content"
                    class="block text-gray-700 text-lg font-bold mb-2"
                    >Content:</label
                >
                <textarea
                    id="content"
                    rows="10"
                    class="w-full px-4 py-3 border rounded border-gray-300 focus:outline-none focus:shadow-outline"
                    bind:value={formData.content}
                ></textarea>
            </div>
            <div class="flex items-center justify-center">
                <button
                    type="submit"
                    class="px-8 py-3 bg-blue-500 text-white rounded hover:bg-blue-600 focus:outline-none"
                    >Submit</button
                >
            </div>
        </form>
    </div>
</div>
