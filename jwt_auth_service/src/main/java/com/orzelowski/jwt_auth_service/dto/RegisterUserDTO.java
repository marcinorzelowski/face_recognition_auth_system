package com.orzelowski.jwt_auth_service.dto;

import lombok.Data;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;

@Data
public class RegisterUserDTO {
    private String username;
    private String password;
}
