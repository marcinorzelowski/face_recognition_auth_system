package com.orzelowski.jwt_auth_service.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.orzelowski.jwt_auth_service.dto.RegisterUserDTO;



import com.orzelowski.jwt_auth_service.service.AuthService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;



@RestController
@CrossOrigin
public class JwtAuthenticationController {

	@Autowired
	private AuthService authService;

	@PostMapping(value = "/signup")
	public boolean addUser(@RequestParam String user, @RequestParam MultipartFile[] images) throws JsonProcessingException {
		return authService.createNewUser(user, images);
	}

	@PostMapping(value = "/authenticate", consumes = "multipart/form-data")
	public ResponseEntity<?> login(@RequestParam String user, @RequestParam MultipartFile image) throws Exception {
		ObjectMapper mapper = new ObjectMapper();
		RegisterUserDTO userDto = mapper.readValue(user, RegisterUserDTO.class);
		return this.authService.authenticate(userDto, image);
	}


}
