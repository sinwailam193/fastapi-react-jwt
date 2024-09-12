import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/_layout/")({
    component: Home,
});

function Home() {
    const data = Route.useLoaderData();

    return <div className="text-red-400">Home route</div>;
}
