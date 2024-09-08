import { createLazyFileRoute } from "@tanstack/react-router";

export const Route = createLazyFileRoute("/_layout/about")({
    component: About,
});

function About() {
    return <div className="text-red-400">About route</div>;
}
