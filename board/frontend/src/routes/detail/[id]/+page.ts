import fastapi from '$lib/api';
import type { PageLoad } from './$types';

interface Question {
    id: number;
    subject: string;
    content: string;
    create_date: string;
}

let question_detail: any = [];

export const load: PageLoad = async ({ params }) => {
    try {
        console.log(params);
        const json = await fastapi('get', '/api/question/detail', params);
        question_detail = json;
        return question_detail;
    } catch (error) {
        console.error('Error fetching question detail:', error);
    }
};
