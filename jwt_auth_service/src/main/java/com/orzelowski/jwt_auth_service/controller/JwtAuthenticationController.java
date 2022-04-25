package com.orzelowski.jwt_auth_service.controller;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;

import com.orzelowski.jwt_auth_service.dto.RegisterUserDTO;
import com.orzelowski.jwt_auth_service.model.ApplicationUser;


import com.orzelowski.jwt_auth_service.service.AuthService;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;

import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;


@RestController
@CrossOrigin
public class JwtAuthenticationController {

	@Autowired
	private AuthService authService;

	@RequestMapping(value = "/signup2", method = RequestMethod.POST)
	public ApplicationUser createUser(@RequestBody RegisterUserDTO registerUserDTO) throws Exception {
		return authService.createNewUser(registerUserDTO);
	}

	@PostMapping(value = "/signup")
	public boolean addUser(@RequestParam String user, @RequestParam MultipartFile[] images) throws JsonProcessingException {
		return authService.createNewUser(user, images);
	}

	@PutMapping(value = "/add-photo/{id}")
	public void addPhoto(@PathVariable Long id, @RequestParam MultipartFile image) throws IOException {
		authService.addPhoto(id, image);
	}


	@PostMapping(value = "/authenticate", consumes = "multipart/form-data")
	public ResponseEntity<?> login(@RequestParam String user, @RequestParam MultipartFile image) throws Exception {
		ObjectMapper mapper = new ObjectMapper();
		RegisterUserDTO userDto = mapper.readValue(user, RegisterUserDTO.class);
		return this.authService.authenticate(userDto, image);
	}


}
