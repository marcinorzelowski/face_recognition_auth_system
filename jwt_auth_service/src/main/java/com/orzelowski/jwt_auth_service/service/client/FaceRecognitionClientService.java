package com.orzelowski.jwt_auth_service.service.client;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;

@Service
public class FaceRecognitionClientService {

    private final WebClient faceRecognitionClient;

    @Value("${face_recognition_service.url}")
    private String url;

    public FaceRecognitionClientService() {
        this.faceRecognitionClient = WebClient.create("http://localhost:5000");
    }

    public Boolean authenticate(MultipartFile image, String username) {
        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("file", image.getResource());
        builder.part("username", username);
        return this.faceRecognitionClient.post()
                .uri("/user")
                .body(BodyInserters.fromMultipartData(builder.build()))
                .retrieve()
                .bodyToMono(Boolean.class)
                .block();
    }

}

