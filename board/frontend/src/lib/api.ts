const fastapi = async (
    operation: string,
    url: string,
    params: any,
    successCallback?: (data: any) => void,
    failureCallback?: (error: any) => void
) => {
    try {
        const baseURL = import.meta.env.VITE_SERVER_URL;
        let endpoint = `${baseURL}${url}`;

        if (operation.toUpperCase() === 'GET') {
            // 만약 params.id가 존재한다면, endpoint에 파라미터를 추가합니다.
            if (params.id) {
                endpoint += `/${params.id}`;
                delete params.id; // id를 endpoint에 추가했으므로 params에서 삭제합니다.
            }
        }
        const options: RequestInit = {
            method: operation.toUpperCase(),
            headers: {
                'Content-Type': 'application/json',
            },
            body:
                operation.toUpperCase() !== 'GET'
                    ? JSON.stringify(params)
                    : undefined,
        };

        const response = await fetch(endpoint, options);
        const data = await response.json();

        if (response.ok || response.status === 204) {
            successCallback?.(data);
            return data;
        } else {
            failureCallback?.(data);
        }
    } catch (error) {
        alert(JSON.stringify(error));
    }
};

export default fastapi;
