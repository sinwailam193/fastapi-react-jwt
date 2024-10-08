/* prettier-ignore-start */

/* eslint-disable */

// @ts-nocheck

// noinspection JSUnusedGlobalSymbols

// This file is auto-generated by TanStack Router

import { createFileRoute } from "@tanstack/react-router";

// Import Routes

import { Route as rootRoute } from "./routes/__root";
import { Route as LayoutImport } from "./routes/_layout";
import { Route as LayoutIndexImport } from "./routes/_layout/index";

// Create Virtual Routes

const LayoutAboutLazyImport = createFileRoute("/_layout/about")();

// Create/Update Routes

const LayoutRoute = LayoutImport.update({
    id: "/_layout",
    getParentRoute: () => rootRoute,
});

const LayoutIndexRoute = LayoutIndexImport.update({
    path: "/",
    getParentRoute: () => LayoutRoute,
}).lazy(() => import("./routes/_layout/index.lazy").then((d) => d.Route));

const LayoutAboutLazyRoute = LayoutAboutLazyImport.update({
    path: "/about",
    getParentRoute: () => LayoutRoute,
}).lazy(() => import("./routes/_layout/about.lazy").then((d) => d.Route));

// Create and export the route tree

export const routeTree = rootRoute.addChildren({
    LayoutRoute: LayoutRoute.addChildren({
        LayoutAboutLazyRoute,
        LayoutIndexRoute,
    }),
});

/* prettier-ignore-end */

/* ROUTE_MANIFEST_START
{
  "routes": {
    "__root__": {
      "filePath": "__root.jsx",
      "children": [
        "/_layout"
      ]
    },
    "/_layout": {
      "filePath": "_layout.jsx",
      "children": [
        "/_layout/about",
        "/_layout/"
      ]
    },
    "/_layout/about": {
      "filePath": "_layout/about.lazy.jsx",
      "parent": "/_layout"
    },
    "/_layout/": {
      "filePath": "_layout/index.jsx",
      "parent": "/_layout"
    }
  }
}
ROUTE_MANIFEST_END */
