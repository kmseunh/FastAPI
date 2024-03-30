import axios, { type AxiosResponse } from 'axios';

interface User {
    user_id: number;
    username: string;
    email: string;
}

export const load: () => Promise<{ users: User[] }> = async () => {
    try {
        const response: AxiosResponse<User[]> = await axios.get(
            'http://localhost:8000/users'
        );
        console.log(response.data);
        return { users: response.data };
    } catch (error) {
        console.error('Error fetching data:', error);
        throw error;
    }
};
