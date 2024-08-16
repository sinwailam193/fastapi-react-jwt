import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/_layout/")({
    component: Home,
});

function Home() {
    return <div className="text-red-400">Home route</div>;
}
