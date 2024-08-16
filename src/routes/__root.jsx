import { lazy, Suspense } from "react";
import { Link, Outlet, createRootRoute } from "@tanstack/react-router";

export const Route = createRootRoute({
    component: Layout,
});

const TanStackRouterDevtools =
    process.env.NODE_ENV === "production"
        ? () => null // Render nothing in production
        : lazy(() =>
              // Lazy load in development
              import("@tanstack/router-devtools").then((res) => ({
                  default: res.TanStackRouterDevtools,
              }))
          );

function Layout() {
    return (
        <div>
            <div>RootRoute</div>
            <div>
                <Link to="/">Home</Link>
                <Link to="/posts">Posts</Link>
            </div>
            <Outlet />
            <Suspense>
                <TanStackRouterDevtools />
            </Suspense>
        </div>
    );
}
