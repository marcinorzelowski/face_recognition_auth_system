package com.orzelowski.jwt_auth_service.service;


import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.orzelowski.jwt_auth_service.config.JwtTokenUtil;
import com.orzelowski.jwt_auth_service.dto.RegisterUserDTO;
import com.orzelowski.jwt_auth_service.errors.FaceNotRecognizedException;
import com.orzelowski.jwt_auth_service.model.ApplicationUser;
import com.orzelowski.jwt_auth_service.model.JwtResponse;
import com.orzelowski.jwt_auth_service.model.UserImage;
import com.orzelowski.jwt_auth_service.repository.ApplicationUserRepository;
import com.orzelowski.jwt_auth_service.repository.UserImageRepository;
import com.orzelowski.jwt_auth_service.service.client.FaceRecognitionClientService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.BadCredentialsException;
import org.springframework.security.authentication.DisabledException;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;

import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.util.Arrays;
import java.util.Objects;

@Service
public class AuthService {

    @Autowired
    private ApplicationUserRepository applicationUserRepository;

    @Autowired
    private PasswordEncoder passwordEncoder;

    @Autowired
    private AuthenticationManager authenticationManager;

    @Autowired
    private JwtTokenUtil jwtTokenUtil;

    @Autowired
    private UserDetailsService userDetailsService;

    @Autowired
    private UserImageRepository userImageRepository;

    @Autowired
    private FaceRecognitionClientService faceRecognitionClientService;


    public ResponseEntity authenticate(RegisterUserDTO registerUserDTO, MultipartFile image) throws Exception {


        authenticate(registerUserDTO.getUsername(), registerUserDTO.getPassword(), image);
        Boolean isRecognized = faceRecognitionClientService.authenticate(image, registerUserDTO.getUsername());
        final UserDetails userDetails = userDetailsService.loadUserByUsername(registerUserDTO.getUsername());
        final String token = jwtTokenUtil.generateToken(userDetails);
        return ResponseEntity.ok(new JwtResponse(token));
    }

    private void authenticate(String username, String password, MultipartFile image) throws Exception {
        try {
            Boolean isRecognized = faceRecognitionClientService.authenticate(image, username);
            if (!isRecognized)
                throw new FaceNotRecognizedException("");
            authenticationManager.authenticate(new UsernamePasswordAuthenticationToken(username, password));
        } catch (DisabledException e) {
            throw new Exception("USER_DISABLED", e);
        } catch (BadCredentialsException e) {
            throw new Exception("INVALID_CREDENTIALS", e);
        }
    }

    public boolean createNewUser(String user, MultipartFile[] images) throws JsonProcessingException {
        ApplicationUser applicationUser = saveUser(user);
        Arrays.stream(images).forEach(multipartFile -> {
            try {
                userImageRepository.save(UserImage.builder()
                        .name(multipartFile.getOriginalFilename())
                        .data(multipartFile.getBytes())
                        .applicationUser(applicationUser)
                        .build());
            } catch (IOException e) {
                e.printStackTrace();
            }
        });
        return true;
    }

    private ApplicationUser saveUser(String userJSON) throws JsonProcessingException {
        ObjectMapper mapper = new ObjectMapper();
        RegisterUserDTO userDto = mapper.readValue(userJSON, RegisterUserDTO.class);
        return applicationUserRepository.save(ApplicationUser.builder()
                .username(userDto.getUsername())
                .password(passwordEncoder.encode(userDto.getPassword()))
                .build());
    }
}
