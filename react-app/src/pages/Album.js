/**
 * @todo
 * this will be a page that will display a single album
 */
import React, { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query'
import { Card, Container, Row, Col, Spinner, Alert } from 'react-bootstrap';
import { API } from '../constants';

function Album() {
    const { id } = useParams();
    const [tracklist, setTracklist] = useState([]);
    
    const { isLoading, data, error } = useQuery({
        queryKey: ['album', id],
        queryFn: async () => {
            const response = await fetch(`${API}albums/${id}`);
            if (!response.ok) {
                throw new Error('Error fetching album');
            }
            return await response.json();
        }
    });

    useEffect(() => {
        const fetchSongs = async () => {
            if (data && data[0]?.tracks.length > 0) {
                const trackPromises = data[0].tracks.map(async (track) => {
                    const response = await fetch(`${API}songs/${track.song}`);
                    if (response.ok) {
                        return await response.json();
                    }
                    return null;
                });

                const songs = await Promise.all(trackPromises);
                setTracklist(songs.filter((song) => song));
            }
        };

        fetchSongs();
    }, [data]);

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
                <Alert variant="danger">
                    Error: {error.message}
                </Alert>
            </Container>
        );
    }

    const album = data[0];

    return (
       <Container className='mt-4'>
            <Row className="justify-content-center">
                <Col 
                md={8} 
                lg={6}>
                    <Card className='shadow-lg'>
                        <Card.Img 
                            variant="top" 
                            src={`http://localhost:8000${album.cover}`} 
                            style={{ borderRadius: '15px 15px 0 0', maxHeight: '400px', objectFit: 'cover' }} 
                        />
                        <Card.Body>
                            <Card.Title className="text-center mb-4" style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>
                                {album.title}
                            </Card.Title>
                            <Card.Text className="text-muted text-center">
                                <strong>Artist:</strong> {album.artist}
                            </Card.Text>
                            <Card.Text className="text-center">
                                <strong>Price:</strong> £{album.price}
                            </Card.Text>
                            <Card.Text className="text-center">
                                <strong>Release Date:</strong> {album.release_date}
                            </Card.Text>
                            <Card.Text className="mt-4" style={{ fontSize: '1rem', lineHeight: '1.5' }}>
                                {album.description}
                            </Card.Text>
                        </Card.Body>
                    </Card>
                </Col>
                <Col>
                    <h4 className='text-center mb-3'>Tracklist</h4>
                    {tracklist.length > 0 ? (
                        <ul>
                            {tracklist.map((song, index) => (
                                <li key={song.id}>
                                    {index + 1}. {song.title}
                                </li>
                            ))}
                        </ul>
                    ) : (
                        <p className="text-center text-muted">No tracks available.</p> 
                    )}
                </Col>
            </Row>
        </Container>
   
    );
}

export default Album;