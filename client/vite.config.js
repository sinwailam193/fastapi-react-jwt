import { defineConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import { TanStackRouterVite } from "@tanstack/router-plugin/vite";

const PORT = 3000;

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [
        TanStackRouterVite({
            quoteStyle: "double",
            disableTypes: true,
            semicolons: true,
        }),
        react(),
    ],
    server: {
        port: PORT,
    },
    preview: {
        port: PORT,
    },
});
