package com.orzelowski.jwt_auth_service.errors;

import javax.naming.AuthenticationException;

public class FaceNotRecognizedException extends AuthenticationException {
    public FaceNotRecognizedException(String msg) {
        super(msg);
    }
}
