package com.orzelowski.jwt_auth_service.repository;

import com.orzelowski.jwt_auth_service.model.UserImage;
import org.springframework.data.jpa.repository.JpaRepository;

public interface UserImageRepository extends JpaRepository<UserImage, Long> {
}
