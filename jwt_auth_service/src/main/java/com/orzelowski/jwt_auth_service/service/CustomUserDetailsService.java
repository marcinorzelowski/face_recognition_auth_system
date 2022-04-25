package com.orzelowski.jwt_auth_service.service;

import com.orzelowski.jwt_auth_service.model.ApplicationUser;
import com.orzelowski.jwt_auth_service.repository.ApplicationUserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;

import java.util.ArrayList;

@Service
public class CustomUserDetailsService implements UserDetailsService {


	@Autowired
	private ApplicationUserRepository applicationUserRepository;

	@Override
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		ApplicationUser applicationUser = applicationUserRepository.findByUsername(username)
				.orElseThrow(() -> new UsernameNotFoundException("User not found."));
		return new User(applicationUser.getUsername(), applicationUser.getPassword(), new ArrayList<>());
	}



}