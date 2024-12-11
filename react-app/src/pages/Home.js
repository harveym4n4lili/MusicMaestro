/**
 * @todo
 * this will be a page that will display a list of albums
 */
import { Card, Container, Row, Col, Spinner } from 'react-bootstrap';
import React from 'react';
import { useQuery } from '@tanstack/react-query'
import { API } from "../constants";
import { Link } from 'react-router-dom';

import './Home.css';

function Home() {
    const { isLoading, data, error } = useQuery({
        queryKey: ['albums'],
        queryFn: async () => {
            const response = await fetch(`${API}albums`)
            return await response.json();
        },
    });
    if (isLoading) {
        return (
            <Container className="text-center my-5">
                <Spinner animation="border" />
                <p>Loading album...</p>
            </Container>
        );
    }

    if (error) {
        return (
            <Container className="text-center my-5">
                Error: {error.message}
            </Container>
        );
    }


    return (
        <div style={{ fontFamily: 'Poppins, sans-serif' }}>
            <Container>
                <Row>
                    {data && data.map((album) => (
                        <Col key={album.id} className="mt-4"
                        sm={12}
                        md={6}
                        lg={4}
                        xl={3}
                        >
                            <Link to={`/albums/${album.id}`} style={{ textDecoration: 'none' }}>
                            <Card 
                            style={{ 
                                borderRadius: '15px',
                                height: '550px',
                                overflowY: 'hidden',
                            }}

                            >
                                <Card.Img   
                                style={{ 
                                    borderRadius: '15px'
                                }}
                                variant="top" 
                                src={`http://localhost:8000${album.cover}`} />
                                <Card.Body>
                                    <Card.Title className='card-title'><strong>{album.title}</strong></Card.Title>
                                    <Card.Text className='card-light-text'>
                                        By {album.artist}<br></br>
                                        {album.release_year}
                                    </Card.Text>
                                    <Card.Text className='card-light-text'>
                                    <strong>£{album.price}</strong>
                                    </Card.Text>
                                    <Card.Text className='card-light-text'  style={{ overflowY: 'auto'}}>
                                        {album.description}
                                    </Card.Text>
                                </Card.Body>
                            </Card>
                            </Link>
                        </Col>
                    ))}
                </Row>
            </Container>
        </div>
    );
}
export default Home;