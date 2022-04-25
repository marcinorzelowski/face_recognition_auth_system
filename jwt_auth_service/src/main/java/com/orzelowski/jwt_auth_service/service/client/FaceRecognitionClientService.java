package com.orzelowski.jwt_auth_service.service.client;

import org.hibernate.service.spi.ServiceException;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.HttpStatus;
import org.springframework.http.client.MultipartBodyBuilder;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;
import org.springframework.web.reactive.function.BodyInserters;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

@Service
public class FaceRecognitionClientService {

    private final WebClient faceRecognitionClient;

    @Value("${face_recognition_service.url}")
    private String url;

    public FaceRecognitionClientService() {
        this.faceRecognitionClient = WebClient.create("http://localhost:5000");
    }


    public void authenticate(MultipartFile image) {
        MultipartBodyBuilder builder = new MultipartBodyBuilder();
        builder.part("file", image.getResource());
        this.faceRecognitionClient.post()
                .uri("/user")
                .body(BodyInserters.fromMultipartData(builder.build()))
                .exchangeToMono(clientResponse -> {
                    if(clientResponse.statusCode().equals(HttpStatus.OK)) {
                        System.out.println("Positivoo");
                        return clientResponse.bodyToMono(Boolean.class).thenReturn(clientResponse.statusCode());
                    } else {
                        throw new ServiceException("Error!");
                    }
                });

    }

    public void test() {
        Mono<String> test = this.faceRecognitionClient.get()
                .uri("/user")
                .retrieve()
                .bodyToMono(String.class)
                        ;

        test.subscribe(System.out::println);
    }
}
