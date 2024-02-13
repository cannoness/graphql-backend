import { createServer } from './core/createServer';

async function startServer() {

    // Create a new instance of the server
    const server = await createServer();

    // Also you can save these values in the .env file
    // Like POST, HOST, ...
    await server.listen({
        port: 3000,
        host: "localhost",
    });

    console.log(`App is running on http://localhost:8080`);
}

// Starting the server ...
(async () => {
    await startServer();
})();