import { createFileRoute, notFound } from "@tanstack/react-router";

export const Route = createFileRoute("/_layout/")({
    loader: async () => {
        const res = fetch("https://jsonplaceholder.typicode.com/posts/1").then(
            (response) => response.json()
        );

        return res;
    },
    pendingComponent: () => <div>data still loading</div>,
});
