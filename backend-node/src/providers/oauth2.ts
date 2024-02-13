import {FastifyInstance, FastifyRegisterOptions, FastifyReply, FastifyRequest} from "fastify";
import OAuth2, {FastifyOAuth2Options, OAuth2Namespace} from "@fastify/oauth2";
import dotenv from 'dotenv';

dotenv.config()
// Register a GoogleOAuth2 namespace globally in the fastify instance
declare module 'fastify' {
    interface FastifyInstance {
        GoogleOAuth2: OAuth2Namespace;
    }
}

// Google OAuth2 Options
const googleOAuth2Options: FastifyRegisterOptions<FastifyOAuth2Options> = {
    // Namespace
    name: '',
    // Scopes
    
  scope: ['openid', 'profile', 'email'],
  //@ts-ignore
  credentials: {
    client: {
      id: process.env.GOOGLE_CLIENT_ID!,
      secret: process.env.GOOGLE_CLIENT_SECRET!
    }
  },
  startRedirectPath: '/login/google',
  callbackUri: 'https://localhost:3000/login/callback',
 
  discovery: {
    issuer: 'https://accounts.google.com/.well-known/openid-configuration'
  },
};

export function registerGoogleOAuth2Provider(app: FastifyInstance) {
    app.register(OAuth2, googleOAuth2Options)
}
